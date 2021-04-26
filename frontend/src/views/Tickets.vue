<template>
  <v-container fluid>
    <v-layout row wrap style="background: #e5e5e5;" class=" events-title mb-3">
      {{ $route.name }}
    </v-layout>

    <v-container class="ma-2 pa-5" fluid>
      <v-data-table
        :headers="headers"
        :items="tickets"
        :search="search"
        height="60vh"
        sort-by="created"
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
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  class="mb-2 ml-2"
                  v-bind="attrs"
                  v-on="on"
                  depressed
                  style="background: #fca311"
                >
                  Add Ticket
                </v-btn>
                <v-text-field
                  v-model="search"
                  append-icon="mdi-magnify"
                  label="Search"
                  class="mb-2 px-2"
                  hide-details
                  style="max-width: 320px;"
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
                        <v-select
                          v-model="editedItem.event_name"
                          :items="event_name_items"
                          item-text="state"
                          item-value="abbr"
                          label="Event Name"
                          return-object
                        ></v-select>
                      </v-col>


                      <v-col
                        cols="12"
                        sm="6"
                        md="6"
                      >
                        <v-text-field
                          v-model="editedItem.no_of_tickets"
                          label="Add More Tickets"
                        ></v-text-field>
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
                    @click.prevent="save()"
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
            @click.prevent="deleteItem(item)"
          >
            mdi-delete
          </v-icon>
        </template>
        <template v-slot:no-data>
          <div>
            No Tickets Issued
          </div>
        </template>
      </v-data-table>
    </v-container>

  </v-container>
</template>

<script>
import { getAPI } from '../main';

  export default {
    name: 'Tickets',
    data: () => ({

      search: "",
      dialog: false,
      dialogDelete: false,
      headers: [
        {
          text: 'Ticket ID',
          align: 'start',
          value: 'id',
        },
        { text: 'Event', value: 'event_name' },
        { text: 'Redeemed', value: 'redeemed' },
        { text: 'Created', value: 'created' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      tickets: [],
      event_name_items: [],
      editedIndex: -1,
      editedItem: {
        event_name: '',
        status: '',
      },
      defaultItem: {
        event_name: '',
        status: '',
      },
    }),

    computed: {
      formTitle () {
        return 'New Ticket'
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

      fetchTickets() {
        getAPI.get('/tickets/')
        .then(response => {
          this.tickets = response.data;
          console.log(response.data)
        })
        .catch(errors => {
          console.log(errors)
        })
      },

      fetchEvents() {
        getAPI.get('/events/')
        .then(response => {
          this.events = response.data;

          for (var i = 0, l = response.data.length; i < l; i++) {
          var obj = response.data[i].event_name;
          this.event_name_items.push(obj)
          }

          console.log(response.data)
        })
        .catch(errors => {
          console.log(errors)
        })
      },

      initialize() {
        this.fetchTickets();
        this.fetchEvents();
      },

      editItem (item) {
        this.editedIndex = this.tickets.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        this.editedIndex = this.tickets.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.tickets.splice(this.editedIndex, 1)

        getAPI.delete('/delete-ticket/' + item.id + '/')
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

          Object.assign(this.event_name[this.editedIndex], this.editedItem)
        
        } else {

          getAPI.post('/create-ticket/', 
                      {event_name: this.editedItem.event_name,
                      no_of_tickets: this.editedItem.no_of_tickets,
                      })
          .then(response => {
            console.log(response);
          })

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

.v-data-table-header-mobile tr th {
  background: #fff;
}


</style>