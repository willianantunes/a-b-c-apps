import { BooleanField, Datagrid, DateField, List, NumberField, ReferenceField, TextField } from 'react-admin'
import * as React from 'react'

export const TodoitemList = () => (
  <List>
    <Datagrid>
      <NumberField source='id' />
      <TextField source='name' />
      <BooleanField source='isComplete' />
      <DateField source='createdAt' showTime={true} />
      <DateField source='updatedAt' showTime={true} />
      <ReferenceField reference='persons' source='person.id' />
    </Datagrid>
  </List>
)
