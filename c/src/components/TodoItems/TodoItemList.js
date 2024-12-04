import { BooleanField, Datagrid, DateField, List, NumberField, ReferenceField, TextField } from 'react-admin'
import * as React from 'react'

export const TodoItemList = ({ properties }) => (
  <List sort={{ field: properties.createdAt, order: 'DESC' }}>
    <Datagrid>
      <NumberField source='id' sortable={false} />
      <TextField source={properties.name} />
      <BooleanField source={properties.isComplete} />
      <DateField source={properties.createdAt} showTime={true} />
      <DateField source={properties.updatedAt} showTime={true} />
      <ReferenceField reference='persons' source={properties.userId} />
    </Datagrid>
  </List>
)
