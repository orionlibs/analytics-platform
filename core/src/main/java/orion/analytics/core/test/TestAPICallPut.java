package orion.analytics.core.test;

import static io.restassured.RestAssured.given;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.parsing.Parser;
import io.restassured.response.Response;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Component;
import orion.analytics.core.utils.Logger;
import orion.analytics.core.utils.JSONUtils;

@Component
class TestAPICallPut
{
    @Autowired private TestHTTPHeader testHTTPHeader;


    Response makePutAPICall(Object objectToSave, HttpHeaders headers)
    {
        Logger.info("[JUnit] making PUT call");
        RestAssured.defaultParser = Parser.JSON;
        headers = testHTTPHeader.getHttpHeaders(headers);
        return given()
                        .contentType(ContentType.JSON)
                        .headers(headers)
                        .accept(ContentType.JSON)
                        .body(JSONUtils.convertObjectToJSON(objectToSave))
                        .when()
                        .put()
                        .then()
                        .extract()
                        .response();
    }
}
