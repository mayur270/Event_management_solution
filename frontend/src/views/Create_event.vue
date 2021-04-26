<template>
	<v-container fluid>
		<v-layout row wrap style="background: #e5e5e5;" class=" events-title mb-0">
		{{ $route.name }}
		</v-layout>

		<v-container fluid class="mt-3">
			<v-layout wrap>
				<v-flex xs12 sm7 md5>
					<v-card elevation="4" light tag="section">
						<v-card-title class="py-5 card-title">
							Add Event Details
						</v-card-title>

						<v-divider></v-divider>

						<v-card-text>
							<v-form class="px-5">
								<v-text-field
									outline
									label="Event Name"
									type="text"
									v-model="event_name"
									prepend-icon="mdi-application"
									required
									@input="$v.event_name.$touch()"
									@blur="$v.event_name.$touch()"
									:error-messages="eventNameError"
									:counter="255"
									>
										
								</v-text-field>
								
								<v-menu
									ref="menu"
									v-model="menu"
									:close-on-content-click="false"
									:return-value.sync="event_date"
									transition="scale-transition"
									offset-y
									min-width="auto"
								>
									<template v-slot:activator="{ on, attrs }">
										<v-text-field
											v-model="event_date"
											label="Date"
											prepend-icon="mdi-calendar"
											readonly
											v-bind="attrs"
											v-on="on"
											required
											@change="$v.event_date.$touch()"
											:error-messages="eventDateError"
										></v-text-field>
									</template>
									<v-date-picker
										v-model="event_date"
										no-title
										scrollable
										:min="calendar_date"
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
											@click="$refs.menu.save(event_date)"
										>
											OK
										</v-btn>
									</v-date-picker>
								</v-menu>

								<v-text-field
									outline
									label="Initial Total Tickets"
									type="text"
									v-model="initial_tickets"
									prepend-icon="mdi-animation-outline"
									required
									@input="$v.initial_tickets.$touch()"
									@blur="$v.initial_tickets.$touch()"
									:error-messages="ticketsError"
								></v-text-field>

								<v-text-field
									outline
									label="Location"
									type="text"
									v-model="event_location"
									prepend-icon="mdi-train-car"
									required
									:counter="255"
									@input="$v.event_location.$touch()"
									@blur="$v.event_location.$touch()"
									:error-messages="eventLocationError"
								></v-text-field>

								<v-select
									v-model="event_status"
									:items="items"
									item-text="state"
									item-value="abbr"
									label="Status"
									return-object
									single-line
									prepend-icon="fas fa-info-circle"
									required
									@change="$v.event_status.$touch()"
									@blur="$v.event_status.$touch()"
									:error-messages="eventStatusError"
								></v-select>

							</v-form>
						</v-card-text>
						<v-divider></v-divider>

						<v-card-actions :class="{ 'pa-4': $vuetify.breakpoint.smAndUp }">
							<v-btn @click="clear" class="px-3">
								Clear
							</v-btn>

							<v-spacer></v-spacer>

							<v-btn style="background: #fca311" @click="submit">
								<v-icon left>fa fa-paper-plane</v-icon>
								Submit
							</v-btn>

						</v-card-actions>
					</v-card>
				</v-flex>
			</v-layout>
		</v-container>

	</v-container>
</template>

<script>
import { getAPI } from '../main';
import { required, maxLength, between } from 'vuelidate/lib/validators'

export default {
    name: 'Create_event',

	validations: {
		event_name: { required, maxLength: maxLength(255) },
		event_date: { required },
		initial_tickets:{ required, between: between(1, 1000)},
		event_location: { required, maxLength: maxLength(255) },
		event_status: { required },
	},

    data: () => ({
		menu: false,
		items: ['OnTime', 'Cancelled', 'Rescheduled'],
		calendar_date: new Date().toISOString().substr(0, 10),
		event_name: '',
		event_date: new Date().toISOString().substr(0, 10),
		initial_tickets: '10',
		event_location: '',
		event_status: 'OnTime',
		
    }),

    computed: {
		eventNameError () {
			const errors = []
			if (!this.$v.event_name.$dirty) return errors
			!this.$v.event_name.maxLength && errors.push('Event Name, at most, can be 255 characters long')
			!this.$v.event_name.required && errors.push('Event Name is required.')
			return errors
		},
		eventDateError () {
			const errors = []
			if (!this.$v.event_date.$dirty) return errors
			!this.$v.event_date.required && errors.push('Date is required.')
			return errors
		},
		ticketsError () {
			const errors = []
			if (!this.$v.initial_tickets.$dirty) return errors
			!this.$v.initial_tickets.between && errors.push('Tickets must be between 1 and 1000')
			!this.$v.initial_tickets.required && errors.push('Tickets is required')
			return errors
		},
		eventLocationError () {
			const errors = []
			if (!this.$v.event_location.$dirty) return errors
			!this.$v.event_location.maxLength && errors.push('Location, at most, can be 255 characters long')
			!this.$v.event_location.required && errors.push('Location is required.')
			return errors
		},
		eventStatusError () {
			const errors = []
			if (!this.$v.event_status.$dirty) return errors
			!this.$v.event_status.required && errors.push('Status is required.')
			return errors
		},
    },

    methods: {

		async submit () {
			this.$v.$touch()

			if (this.$v.$pending || this.$v.$error) return;

			await getAPI.post('/create-event/', 
				{event_name: this.event_name,
				event_date: this.event_date,
				initial_tickets: this.initial_tickets,
				event_location: this.event_location,
				event_status: this.event_status})
			.then(response => {
				console.log(response);
			})

			alert("Form submitted");

			this.$router.push('/events/')
		},

		clear () {
			this.event_name = ''
			this.event_date = null
			this.initial_tickets = ''
			this.event_location = ''
			this.event_status = null
			this.$refs.observer.reset()
			},
		},
}

</script>

<style scoped>
.card-title {
	font-size: 1.2rem;
	background: #14213d; 
	color: #fca311;
}

</style>
    
