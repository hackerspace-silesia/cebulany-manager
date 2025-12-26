<template>
  <div class="documents">
    <b-table
      hover="hover"
      bordered="bordered"
      small="small"
      foot-clone="foot-clone"
      :items="documents"
      :fields="fields"
      :tbody-tr-class="rowClass"
    >
      <template v-slot:cell(additional)="row">
        <b-form>
          <b-form-group label-cols="2" label="Nazwa pliku">
            <b-form-input
              v-model.lazy.trim="row.item.filename"
              size="sm"
              @change="update(row.item)"
            />
          </b-form-group>
          <b-form-group label-cols="2" label="Numer dok.">
            <b-form-input
              v-model.lazy.trim="row.item.accounting_record"
              size="sm"
              @change="update(row.item)"
            />
          </b-form-group>
          <b-form-group label-cols="2" label="Data dok.">
            <date-picker
              v-model="row.item.accounting_date"
              type="date"
              value-type="format"
              token="YYYY-MM-DD"
              clearable
              @change="update(row.item)"
            />
          </b-form-group>
          <b-form-group label-cols="2" label="Nazwa firmy">
            <b-form-input
              v-model.lazy.trim="row.item.company_name"
              size="sm"
              @change="update(row.item)"
            />
          </b-form-group>
          <b-form-group label-cols="2" label="Kwota">
            <b-form-input
              v-model.lazy.trim="row.item.price"
              type="number"
              step="0.01"
              size="sm"
              @change="update(row.item)"
            />
          </b-form-group>
        </b-form>
      </template>
      <template v-slot:cell(description)="row">
        <b-form-textarea
          v-model.lazy.trim="row.item.description"
          rows="3"
          max-rows="6"
          wrap="hard"
          size="sm"
          @change="update(row.item)"
        />
      </template>
      <template v-slot:cell(link)="row">
        <b-btn @click="show(row.item)" size="sm">Link</b-btn>
      </template>
    </b-table>
  </div>
</template>
<script>
  export default {
    props: ['documents', 'itemToShow'],
    data () {
      return {
        fields: [
          {key: 'additional', label: 'Pola'},
          {key: 'description', label: 'Opis'},
          {key: 'link', label: 'Podgląd'},
        ]
      }
    },
    methods: {
      update (row) {
        this.$emit('row-update', row);
      },
      show (item) {
        this.$emit('row-show', {id: item.id, label: item.filename, link: item.link});
      },
      rowClass (item, type) {
        if (!item || type !== 'row' || !this.itemToShow) {
          return;
        }
        if (item.id === this.itemToShow.id) {
          return 'table-primary';
        }
      },
    }
  }
</script>
