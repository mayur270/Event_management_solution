<template>
  <v-container fluid>
    <v-layout row wrap style="background: #e5e5e5;" class=" events-title mb-3">
      {{ $route.name }}
    </v-layout>

    <v-container class="ma-2 pa-5" fluid>
      <v-data-table
        :headers="headers"
        :items="event_name"
        :search="search"
        height="60vh"
        sort-by="date"
        class="eventTable"
      >
        <template v-slot:top>
          <v-toolbar
            flat
          >
            <v-spacer></v-spacer>
            <v-dialog
              v-model="dialog"
              max-width="500px"
            >
              <template v-slot:activator="{}">
                <v-btn
                  class="mb-2 ml-2"
                  depressed
                  color="#fca311"
                  @click.prevent="fetchTasks()"
                >
                  <v-icon small>fas fa-sync-alt</v-icon>
                </v-btn>
                <v-text-field
                  v-model="search"
                  append-icon="mdi-magnify"
                  label="Search"
                  class="mb-2 px-2"
                  hide-details
                  style="max-width: 350px;"
                >Search</v-text-field>
              </template>
              <v-card>
                <v-card-title>
                  <span class="headline">{{ formTitle }}</span>
                </v-card-title>

                <v-card-text>
                  <v-container>
                    <v-row>

                      <v-col
                        cols="12"
                        sm="6"
                        md="6"
                      >
                        <v-text-field
                          v-model="editedItem.event_name"
                          label="Event Name"
                          disabled
                        ></v-text-field>
                      </v-col>

                      <v-col
                        cols="12"
                        sm="6"
                        md="6"
                      >
                        <v-text-field
                          v-model="editedItem.event_location"
                          label="Location"
                          disabled
                        ></v-text-field>
                      </v-col>

                      <v-col
                        cols="12"
                        sm="6"
                        md="6"
                      >
                        <v-menu
                          ref="menu"
                          v-model="menu"
                          :close-on-content-click="false"
                          :return-value.sync="editedItem.event_date"
                          transition="scale-transition"
                          offset-y
                          min-width="auto"
                        >
                          <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                              v-model="editedItem.event_date"
                              label="Date"
                              prepend-icon="mdi-calendar"
                              readonly
                              v-bind="attrs"
                              v-on="on"
                            ></v-text-field>
                          </template>
                          <v-date-picker
                            v-model="editedItem.event_date"
                            no-title
                            scrollable
                            :min="defaultItem.event_date"
                          >
                            <v-spacer></v-spacer>
                            <v-btn
                              text
                              color="primary"
                              @click="menu = false"
                            >
                              Cancel
                            </v-btn>
                            <v-btn
                              text
                              color="primary"
                              @click="$refs.menu.save(editedItem.event_date)"
                            >
                              OK
                            </v-btn>
                          </v-date-picker>
                        </v-menu>
                      </v-col>

                      <v-col 
                        cols="12"
                        xs="12" 
                        sm="6"
                        md="6"
                      >
                        <v-select
                          v-model="editedItem.event_status"
                          :items="items"
                          item-text="state"
                          item-value="abbr"
                          label="Status"
                          return-object
                        ></v-select>
                      </v-col>

                    </v-row>
                  </v-container>
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="blue darken-1"
                    text
                    @click="close"
                  >
                    Cancel
                  </v-btn>
                  <v-btn
                    color="blue darken-1"
                    text
                    @click="save"
                  >
                    Save
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-icon
            small
            class="mr-2"
            @click="editItem(item)"
          >
            mdi-pencil
          </v-icon>
          <v-icon
          small
          @click="deleteItem(item)"
        >
          mdi-delete
        </v-icon>
        </template>
        <template v-slot:no-data>
          <div>
            No Events
          </div>
        </template>
      </v-data-table>

    </v-container>

  </v-container>
</template>

<script>
import {getAPI} from '../main';

  export default {
    name: 'Events',
    components: {
      
    },
    data: () => ({

      search: '',
      dialog: false,
      headers: [
        {
          text: 'Event Name',
          align: 'start',
          value: 'event_name',
        },
        { text: 'Date', value: 'event_date', },
        { text: 'Total Tickets', value: 'event_ticket_count' },
        { text: 'Redeemed Tickets', value: 'redeemed_ticket_count' },
        { text: 'Location', value: 'event_location' },
        { text: 'Status', value: 'event_status' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      event_name: [],
      editedIndex: -1,
      editedItem: {
        event_name: '',
        event_date: new Date().toISOString().substr(0, 10),
        initial_tickets: 100,
        event_location: 0,
        event_status: 0,
      },
      defaultItem: {
        event_name: '',
        event_date: new Date().toISOString().substr(0, 10),
        initial_tickets: 100,
        event_location: 'London',
        event_status: 'OnTime',
      },
      menu: false,
      items: ['OnTime', 'Rescheduled', 'Cancelled']
    }),

    computed: {
      formTitle () {
        return 'Edit Event'
      },
    },

    watch: {
      dialog (val) {
        val || this.close()
      },
    },

    created () {
      this.initialize()
    },

    methods: {

      fetchTasks() {
        getAPI.get('/events/')
        .then(response => {
          this.event_name = response.data;

          console.log(response)
        })
        .catch(errors => {
          console.log(errors)
        })
      },

      initialize() {
        this.fetchTasks();
      },

      refreshPage() {
        window.location.reload();
      },

      editItem (item) {
        this.editedIndex = this.event_name.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        this.editedIndex = this.event_name.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.event_name.splice(this.editedIndex, 1)

        getAPI.delete('/delete-event/' + item.id)
          .then(response => {
            console.log(response);
          })
          .catch(errors => {
            console.log(errors)
          })
      },

      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      save () {
        if (this.editedIndex > -1) {

          getAPI.put('/edit-event/' + this.editedItem.id + '/', 
              {event_date: this.editedItem.event_date,
               event_status: this.editedItem.event_status,
               event_name: this.editedItem.event_name,
               event_location: this.editedItem.event_location})

          .then(response => {
            console.log(response);
          })
          .catch(errors => {
            console.log(errors)
          })

          Object.assign(this.event_name[this.editedIndex], this.editedItem)
        
        } else {

          this.event_name.push(this.editedItem)
        }

        this.close()
      },

    },

  }
</script>

<style>

@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic&display=swap');

.events-title {
  font-family: 'Pacifico', cursive;
  padding: 0.5em 0.8em;
  font-size: 2.5em;
  color: #023047;
}

/* Data table */

.eventTable td {
    border-bottom: none !important;
    padding: 25px 20px !important;

}

.eventTable tr:hover:not(.v-table__expanded__content) {
  background-color: none !important;
}

 tbody tr:nth-of-type(odd) {
  background-color: rgba(0, 0, 0, .05);
}

.v-data-footer {
  background-color: rgb(250 ,250, 250);
}

.eventTable th {
  font-family: 'Nanum Gothic', sans-serif;
  font-size: 36px;
  color: #fff !important;
  line-height: 1.4;
  text-transform: uppercase;

  background-color: #14213d;
}

v-data-table-header v-data-table-header-mobile {
  background: #fff;
}

.v-data-table-header-mobile tr th{
  background: #fff;
}


</style>