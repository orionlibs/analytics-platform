package orion.analytics.metrics;

import java.util.Set;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Builder
@Data
public class Metric
{
    private String name;
    private String description;
    private String type;
    private Set<MetricTag> tags;
}
