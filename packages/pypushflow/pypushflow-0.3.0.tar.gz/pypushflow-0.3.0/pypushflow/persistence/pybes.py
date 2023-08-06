import os
from typing import Optional
from .pymongo import PyMongoWorkflowDbClient

try:
    from bson.objectid import ObjectId
except Exception:
    ObjectId = None


class PyBesWorkflowDbClient(PyMongoWorkflowDbClient, register_name="pybes"):
    """Client of the PyBes Mongo database for storing workflow executions."""

    def connect(self, url: Optional[str] = None):
        if not url:
            url = os.environ.get("PYPUSHFLOW_MONGOURL", None)
        super().connect(url=url, database="pybes", collection="pybes")

    def _generateInitialWorkflowInfo(self) -> dict:
        initiator = os.environ.get("PYPUSHFLOW_INITIATOR", "Unknown")
        host = os.environ.get("PYPUSHFLOW_HOST", "Unknown")
        port = os.environ.get("PYPUSHFLOW_PORT", "Unknown")
        requestId = os.environ.get("PYPUSHFLOW_OBJECTID", "Unknown")
        initial_workflow_info = {
            "initiator": initiator,
            "host": host,
            "port": port,
            "Request ID": requestId,
        }
        if requestId != "Unknown":
            initial_workflow_info["_id"] = ObjectId(requestId)
        return initial_workflow_info

    def generateWorkflowId(self, oid: Optional[str] = None):
        if not oid:
            oid = os.environ.get("PYPUSHFLOW_OBJECTID")
        super().generateWorkflowId(oid=oid)
