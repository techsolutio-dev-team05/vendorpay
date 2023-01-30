import json
import logging
import grpc
from zeebe_grpc import gateway_pb2, gateway_pb2_grpc

with grpc.insecure_channel("localhost:26500") as channel:
    stub = gateway_pb2_grpc.GatewayStub(channel)

    # print the topology of the zeebe cluster
    # topology = stub.Topology(gateway_pb2.TopologyRequest())
    # print(topology)

    # deploy a process definition
    with open("/home/alfaer/Documents/camunda/Preparing Dinner.bpmn", "rb") as process_definition_file:
        process_definition = process_definition_file.read()
        process = gateway_pb2.ProcessRequestObject(
            name="Preparing Dinner.bpmn",
            definition=process_definition)
        
        stub.DeployProcess(
            gateway_pb2.DeployProcessRequest(
            processes=[process]
        )
    )

    # start a process instance
    variables = {"entrada": 5}
    stub.CreateProcessInstance(
        gateway_pb2.CreateProcessInstanceRequest(
            bpmnProcessId="preparing-dinner",
            version=-1,
            variables=json.dumps(variables)
        )
    )

    # # start a worker
    # activate_jobs_response = stub.ActivateJobs(
    #     gateway_pb2.ActivateJobsRequest(
    #         type="orchestrate-something",
    #         worker="Python worker",
    #         timeout=60000,
    #         maxJobsToActivate=32
    #     )
    # )
    # for response in activate_jobs_response:
    #     for job in response.jobs:
    #         try:
    #             print(job.variables)
    #             stub.CompleteJob(gateway_pb2.CompleteJobRequest(jobKey=job.key, variables=json.dumps({"saida": 6})))
    #             logging.info("Job Completed")
    #         except Exception as e:
    #             stub.FailJob(gateway_pb2.FailJobRequest(jobKey=job.key))
    #             logging.info(f"Job Failed {e}")
