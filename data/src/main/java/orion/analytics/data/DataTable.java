package orion.analytics.data;

import java.util.Set;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Builder
@Data
public class DataTable
{
    private String name;
    private String description;
    private Set<DataTableColumn> columns;
}
