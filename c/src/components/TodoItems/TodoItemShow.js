import { BooleanField, DateField, Show, SimpleShowLayout, TextField } from 'react-admin'

export const TodoItemShow = () => (
  <Show>
    <SimpleShowLayout>
      <TextField source='id' />
      <TextField source='name' />
      <BooleanField source='isComplete' />
      <DateField source='createdAt' showTime={true} />
      <DateField source='updatedAt' showTime={true} />
    </SimpleShowLayout>
  </Show>
)
