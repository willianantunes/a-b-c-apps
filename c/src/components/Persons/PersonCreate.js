import * as React from 'react'
import { Create, required, SimpleForm, TextInput } from 'react-admin'

export const PersonCreate = ({ properties }) => (
  <Create redirect='list'>
    <SimpleForm>
      <TextInput source={properties.name} validate={[required()]} />
    </SimpleForm>
  </Create>
)
