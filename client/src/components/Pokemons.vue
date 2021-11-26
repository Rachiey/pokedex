<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>pokemons</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.pokemon-modal>Add New</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Type</th>
              <th scope="col">Caught?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(pokemon, index) in pokemons" :key="index">
              <td>{{ pokemon.name }}</td>
              <td>{{ pokemon.pokeType }}</td>
              <td>
                <span v-if="pokemon.caught">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.pokemon-update-modal
                          @click="editpokemon(pokemon)">
                      Update
                  </button>
                  <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeletepokemon(pokemon)">
                      Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addpokemonModal"
            id="pokemon-modal"
            name="Add a new pokemon"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-name-group"
                    label="Enter pokemon name:"
                    label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addpokemonForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-pokeType-group"
                      label="Type:"
                      label-for="form-pokeType-input">
            <b-form-input id="form-pokeType-input"
                          type="text"
                          v-model="addpokemonForm.pokeType"
                          required
                          placeholder="Enter Type">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-caught-group">
          <b-form-checkbox-group v-model="addpokemonForm.caught" id="form-checks">
            <b-form-checkbox value="true">caught?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editpokemonModal"
            id="pokemon-update-modal"
            name="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-name-edit-group"
                    label="name:"
                    label-for="form-name-edit-input">
          <b-form-input id="form-name-edit-input"
                        type="text"
                        v-model="editForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-pokeType-edit-group"
                      label="Type:"
                      label-for="form-pokeType-edit-input">
            <b-form-input id="form-pokeType-edit-input"
                          type="text"
                          v-model="editForm.pokeType"
                          required
                          placeholder="Enter pokeType">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-caught-edit-group">
          <b-form-checkbox-group v-model="editForm.caught" id="form-checks">
            <b-form-checkbox value="true">caught?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      pokemons: [],
      addpokemonForm: {
        name: '',
        pokeType: '',
        caught: [],
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        name: '',
        pokeType: '',
        caught: [],
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getpokemons() {
      const path = 'http://localhost:5000/pokemons';
      axios.get(path)
        .then((res) => {
          this.pokemons = res.data.pokemons;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addpokemon(payload) {
      const path = 'http://localhost:5000/pokemons';
      axios.post(path, payload)
        .then(() => {
          this.getpokemons();
          this.message = 'Pokemon added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getpokemons();
        });
    },
    initForm() {
      this.addpokemonForm.name = '';
      this.addpokemonForm.pokeType = '';
      this.addpokemonForm.caught = [];
      this.editForm.id = '';
      this.editForm.name = '';
      this.editForm.pokeType = '';
      this.editForm.caught = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addpokemonModal.hide();
      let caught = false;
      if (this.addpokemonForm.caught[0]) caught = true;
      const payload = {
        name: this.addpokemonForm.name,
        pokeType: this.addpokemonForm.pokeType,
        caught, // property shorthand
      };
      this.addpokemon(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addpokemonModal.hide();
      this.initForm();
    },
    editpokemon(pokemon) {
      this.editForm = pokemon;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editpokemonModal.hide();
      let caught = false;
      if (this.editForm.caught[0]) caught = true;
      const payload = {
        name: this.editForm.name,
        pokeType: this.editForm.pokeType,
        caught,
      };
      this.updatepokemon(payload, this.editForm.id);
    },
    updatepokemon(payload, pokemonID) {
      const path = `http://localhost:5000/pokemons/${pokemonID}`;
      axios.put(path, payload)
        .then(() => {
          this.getpokemons();
          this.message = 'pokemon updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getpokemons();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editpokemonModal.hide();
      this.initForm();
      this.getpokemons(); // why?
    },
    removepokemon(pokemonID) {
      const path = `http://localhost:5000/pokemons/${pokemonID}`;
      axios.delete(path)
        .then(() => {
          this.getpokemons();
          this.message = 'pokemon removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getpokemons();
        });
    },
    onDeletepokemon(pokemon) {
      this.removepokemon(pokemon.id);
    },
  },
  created() {
    this.getpokemons();
  },
};
</script>
