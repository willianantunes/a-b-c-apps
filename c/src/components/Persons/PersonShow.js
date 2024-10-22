import {
  BooleanField,
  Datagrid,
  DateField,
  NumberField,
  ReferenceManyField,
  Show,
  TabbedShowLayout,
  TextField,
} from 'react-admin'
import * as React from 'react'
import { CreateRelatedTodoItemButton } from '@/components/Persons/PersonEdit'

export const PersonShow = () => (
  <Show>
    <TabbedShowLayout>
      <TabbedShowLayout.Tab label='Person'>
        <TextField source='name' />
        <DateField source='createdAt' showTime={true} />
        <DateField source='updatedAt' showTime={true} />
        <TextField source='id' />
      </TabbedShowLayout.Tab>
      <TabbedShowLayout.Tab label='Todo items'>
        <ReferenceManyField reference='todoitems' target='userId'>
          <Datagrid>
            <TextField source='name' />
            <BooleanField source='isComplete' />
            <DateField source='createdAt' showTime={true} />
            <DateField source='updatedAt' showTime={true} />
            <NumberField source='id' />
          </Datagrid>
        </ReferenceManyField>
        <CreateRelatedTodoItemButton />
      </TabbedShowLayout.Tab>
    </TabbedShowLayout>
  </Show>
)
