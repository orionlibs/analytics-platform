package orion.analytics.core.test;

import static io.restassured.RestAssured.given;
import orion.analytics.core.Logger;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.parsing.Parser;
import io.restassured.response.Response;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Component;

@Component
class TestAPICallDelete
{
    @Autowired private TestHTTPHeader testHTTPHeader;


    Response makeDeleteAPICall(HttpHeaders headers)
    {
        Logger.info("[JUnit] making DELETE call");
        RestAssured.defaultParser = Parser.JSON;
        headers = testHTTPHeader.getHttpHeaders(headers);
        return given()
                        .contentType(ContentType.JSON)
                        .headers(headers)
                        .accept(ContentType.JSON)
                        .when()
                        .delete()
                        .then()
                        .extract()
                        .response();
    }
}
