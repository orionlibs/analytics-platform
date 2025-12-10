package orion.analytics.core.test;

import io.restassured.response.Response;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Component;

@Component
public class APITestUtils
{
    @Autowired private TestAPICallGet testAPICallGet;
    @Autowired private TestAPICallPost testAPICallPost;
    @Autowired private TestAPICallPut testAPICallPut;
    @Autowired private TestAPICallPatch testAPICallPatch;
    @Autowired private TestAPICallDelete testAPICallDelete;


    public Response makeGetAPICall(HttpHeaders headers)
    {
        return testAPICallGet.makeGetAPICall(headers);
    }


    public Response makePostAPICall(Object objectToSave, HttpHeaders headers)
    {
        return testAPICallPost.makePostAPICall(objectToSave, headers);
    }


    public Response makePutAPICall(Object objectToSave, HttpHeaders headers)
    {
        return testAPICallPut.makePutAPICall(objectToSave, headers);
    }


    public Response makePatchAPICall(Object objectToSave, HttpHeaders headers)
    {
        return testAPICallPatch.makePatchAPICall(objectToSave, headers);
    }


    public Response makeDeleteAPICall(HttpHeaders headers)
    {
        return testAPICallDelete.makeDeleteAPICall(headers);
    }
}
