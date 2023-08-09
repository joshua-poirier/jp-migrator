import azure.functions as func
import logging

app = func.FunctionApp()


@app.function_name(name="HttpTrigger2")
@app.route(route="hello")
def test_function2(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get("name", "")

    return func.HttpResponse(f"HttpTrigger2 function processed {name}'s request")
