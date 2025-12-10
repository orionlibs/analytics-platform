package orion.analytics.app.configuration;

import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.Ordered;
import orion.analytics.core.api.filter.TraceFilter;
import orion.analytics.core.api.filter.UserIDFilter;

@Configuration
public class HTTPFilterConfiguration
{
    @Bean
    public FilterRegistrationBean<TraceFilter> traceFilterRegistration(TraceFilter traceFilter)
    {
        FilterRegistrationBean<TraceFilter> registration = new FilterRegistrationBean<>();
        registration.setFilter(traceFilter);
        registration.setOrder(Ordered.HIGHEST_PRECEDENCE);
        registration.addUrlPatterns("/*");
        return registration;
    }


    @Bean
    public FilterRegistrationBean<UserIDFilter> userIDFilterRegistration(UserIDFilter userIDFilter)
    {
        FilterRegistrationBean<UserIDFilter> registration = new FilterRegistrationBean<>();
        registration.setFilter(userIDFilter);
        registration.setOrder(Ordered.HIGHEST_PRECEDENCE + 1);
        registration.addUrlPatterns("/*");
        return registration;
    }
}
