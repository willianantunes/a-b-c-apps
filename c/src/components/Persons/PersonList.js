import { Datagrid, DateField, List, TextField, NumberField } from 'react-admin'

export const PersonList = () => (
  <List>
    <Datagrid>
      <NumberField source='id' />
      <TextField source='name' />
      <DateField source='createdAt' showTime={true} />
      <DateField source='updatedAt' showTime={true} />
    </Datagrid>
  </List>
)
