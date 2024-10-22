import { BooleanInput, DateInput, Edit, SimpleForm, TextInput } from 'react-admin'
import * as React from 'react'

export const TodoItemEdit = () => (
  <Edit>
    <SimpleForm>
      <TextInput source='name' />
      <BooleanInput source='isComplete' />
      <DateInput source='createdAt' InputProps={{ disabled: true }} />
      <DateInput source='updatedAt' InputProps={{ disabled: true }} />
      <TextInput source='id' InputProps={{ disabled: true }} />
    </SimpleForm>
  </Edit>
)
