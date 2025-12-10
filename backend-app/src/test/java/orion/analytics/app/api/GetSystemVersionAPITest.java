package orion.analytics.app.api;

import static org.assertj.core.api.Assertions.assertThat;

import io.restassured.RestAssured;
import io.restassured.common.mapper.TypeRef;
import io.restassured.response.Response;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.http.HttpHeaders;
import org.springframework.test.context.ActiveProfiles;
import orion.analytics.app.TestBase;
import orion.analytics.app.api.GetSystemVersionAPI.Version;
import orion.analytics.core.api.APIResponse;
import orion.analytics.core.test.APITestUtils;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
class GetSystemVersionAPITest extends TestBase
{
    @LocalServerPort int port;
    @Autowired APITestUtils apiUtils;
    HttpHeaders headers;


    @BeforeEach
    void setUp()
    {
        addPortToAPIEndpoint(port);
        headers = new HttpHeaders();
        RestAssured.baseURI = apiEndpointPrefix;
    }


    @Test
    void getProjectTypes()
    {
        RestAssured.baseURI += "/system/version";
        Response response = apiUtils.makeGetAPICall(headers);
        assertThat(response.statusCode()).isEqualTo(200);
        APIResponse<Version> body = response.as(new TypeRef<APIResponse<GetSystemVersionAPI.Version>>()
        {
        });
        assertThat(body.getData().getVersion()).isEqualTo("0.0.1");
    }
}
