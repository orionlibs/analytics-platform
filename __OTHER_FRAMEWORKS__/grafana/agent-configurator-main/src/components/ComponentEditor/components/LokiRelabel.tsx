import { FormAPI, InlineField, Input } from "@grafana/ui";
import ReferenceMultiSelect from "../inputs/ReferenceMultiSelect";
import { RelabelRules, transformRules } from "../common/RelabelRules";

const Component = ({ methods }: { methods: FormAPI<Record<string, any>> }) => {
  return (
    <>
      <InlineField
        label="Forward to"
        tooltip="Where to forward log entries after relabeling."
        labelWidth={22}
        error="You must specify a list of destinations"
        invalid={!!methods.errors["targets"]}
      >
        <ReferenceMultiSelect
          name="forward_to"
          exportName="LokiReceiver"
          control={methods.control}
        />
      </InlineField>
      <InlineField
        label="Max cache size"
        tooltip="The maximum number of elements to hold in the relabeling cache."
        labelWidth={22}
      >
        <Input type="number" {...methods.register("max_cache_size")} />
      </InlineField>
      <RelabelRules methods={methods} />
    </>
  );
};

const LokiRelabel = {
  preTransform(data: Record<string, any>): Record<string, any> {
    return data;
  },
  postTransform(data: Record<string, any>): Record<string, any> {
    return transformRules(data);
  },
  Component,
};
export default LokiRelabel;
