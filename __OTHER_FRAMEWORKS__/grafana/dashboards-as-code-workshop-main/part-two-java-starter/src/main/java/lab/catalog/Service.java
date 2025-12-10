package lab.catalog;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Service {
    public String name;
    public String description;
    @JsonProperty("has_http")
    public boolean hasHttp;
    @JsonProperty("has_grpc")
    public boolean hasGrpc;
    @JsonProperty("github")
    public String repositoryUrl;
}
