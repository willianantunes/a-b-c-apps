import { BooleanField, DateField, ReferenceField, Show, SimpleShowLayout, TextField } from 'react-admin'
import * as React from 'react'

export const TodoItemShow = ({ properties }) => (
  <Show>
    <SimpleShowLayout>
      <TextField source='id' />
      <TextField source={properties.name} />
      <BooleanField source={properties.isComplete} />
      <DateField source={properties.createdAt} showTime={true} />
      <DateField source={properties.updatedAt} showTime={true} />
      <ReferenceField reference='persons' source={properties.userId} />
    </SimpleShowLayout>
  </Show>
)
