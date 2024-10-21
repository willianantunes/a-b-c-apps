import * as React from 'react'
import { Create, required, SimpleForm, TextInput } from 'react-admin'

export const PersonCreate = () => (
  <Create redirect='list'>
    <SimpleForm>
      <TextInput source='name' validate={[required()]} />
    </SimpleForm>
  </Create>
)
