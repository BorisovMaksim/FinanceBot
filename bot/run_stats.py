import os
import asyncio

from dff.script import Context
from dff.messengers.telegram import PollingTelegramInterface
from dff.pipeline import (
    Pipeline,
    ACTOR,
    Service,
    ExtraHandlerRuntimeInfo,
    ServiceGroup,
    GlobalExtraHandlerType,
)

from dialog_graph import script
from pipeline_services import pre_services
from dff.context_storages import context_storage_factory
from dff.stats import (
    OtelInstrumentor,
    set_logger_destination,
    set_tracer_destination,
)
from dff.stats import OTLPLogExporter, OTLPSpanExporter
from dff.stats import default_extractors
from dff.stats.utils import get_wrapper_field

from dotenv import load_dotenv

import datetime



set_logger_destination(OTLPLogExporter("grpc://localhost:4317", insecure=True))
set_tracer_destination(OTLPSpanExporter("grpc://localhost:4317", insecure=True))
dff_instrumentor = OtelInstrumentor()
dff_instrumentor.instrument()



async def get_timing_before(ctx: Context, _, info: ExtraHandlerRuntimeInfo):
    start_time = datetime.now()
    ctx.misc[get_wrapper_field(info, "time")] = start_time



async def get_timing_after(ctx: Context, _, info: ExtraHandlerRuntimeInfo):  # noqa: F811
    start_time = ctx.misc[get_wrapper_field(info, "time")]
    data = {"execution_time": str(datetime.now() - start_time)}
    return data



@dff_instrumentor
async def get_service_state(ctx: Context, _, info: ExtraHandlerRuntimeInfo):
    data = {
        "execution_state": info.component.execution_state,
    }
    return data



async def heavy_service(ctx: Context):
    _ = ctx 
    await asyncio.sleep(0.02)



def get_pipeline(use_cli_interface: bool = False) -> Pipeline:
    telegram_token = os.getenv("TG_BOT_TOKEN")

    if use_cli_interface:
        messenger_interface = None
    elif telegram_token:
        messenger_interface = PollingTelegramInterface(token=telegram_token)
    else:
        raise RuntimeError(
            "Telegram token (`TG_BOT_TOKEN`) is not set. `TG_BOT_TOKEN` can be set via `.env` file."
            " For more info see README.md."
        )
    postgresql_envs =  ["POSTGRES_USERNAME", "POSTGRES_PASSWORD", "POSTGRES_DB"] 
    if any([env not in  os.environ  for env in postgresql_envs]):
        raise RuntimeError(
            f"Postgresql tokens (`{postgresql_envs}`) are not set"
        )
        
    db_uri = "postgresql+asyncpg://{}:{}@localhost:5432/{}".format(
        os.environ["POSTGRES_USERNAME"],
        os.environ["POSTGRES_PASSWORD"],
        os.environ["POSTGRES_DB"],
)
    db = context_storage_factory(db_uri)
    pipeline = Pipeline.from_dict(
        {
        "script": script.script,
        "start_label": ("service_flow", "start_node"),
        "fallback_label": ("service_flow", "fallback_node"),
        "messenger_interface":messenger_interface,
        "context_storage": db,
        "components": [
            ServiceGroup(
                before_handler=[get_timing_before],
                after_handler=[
                    get_service_state,
                    get_timing_after,
                ],
                components=[
                    {"handler": heavy_service},
                    {"handler": heavy_service},
                ],
            ),
            pre_services.services,        
            Service(
                handler=ACTOR,
                before_handler=[
                    get_timing_before,
                ],
                after_handler=[
                    get_service_state,
                    default_extractors.get_current_label,
                    get_timing_after,
                ],
            ),
        ],
    }
)
    pipeline.add_global_handler(
    GlobalExtraHandlerType.BEFORE_ALL, get_timing_before
    )
    pipeline.add_global_handler(
    GlobalExtraHandlerType.AFTER_ALL, get_timing_after
    )
    pipeline.add_global_handler(GlobalExtraHandlerType.AFTER_ALL, get_service_state)

    return pipeline



if __name__ == "__main__":
    load_dotenv()
    pipeline = get_pipeline()
    pipeline.run()
 