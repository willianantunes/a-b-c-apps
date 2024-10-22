import { Datagrid, DateField, List, TextField, NumberField, TextInput } from 'react-admin'

const personFilters = [
  // `_interceptChangeToSearch` is a special source.
  // Check the implementation in `ra-data-ndjango-rest-framework-pagination` for more details.
  <TextInput source='_interceptChangeToSearch' label='Search by name' alwaysOn />,
]

export const PersonList = () => (
  <List filters={personFilters}>
    <Datagrid>
      <NumberField source='id' />
      <TextField source='name' />
      <DateField source='createdAt' showTime={true} />
      <DateField source='updatedAt' showTime={true} />
    </Datagrid>
  </List>
)
