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
            <b-input-group size="sm">
              <b-form-input
                v-model.lazy.trim="row.item.filename"
                @change="update(row.item)"
              />
              <b-input-group-append>
                <b-button variant="info" @click="generateFilename(row.item)">Generuj</b-button>
              </b-input-group-append>
            </b-input-group>
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
      <template v-slot:cell(actions)="row">
        <b-btn @click="show(row.item)" variant="primary" size="sm">Podgląd</b-btn>
        <b-btn @click="remove(row.item)" variant="danger" size="sm">Usuń</b-btn>
        <br />
        <b-badge v-if="row.item._state === 'loading'" pill variant="warning">Loading</b-badge>
        <b-badge v-if="row.item._state === 'error'" pill variant="loading">Error</b-badge>
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
          {key: 'actions', label: 'Akcje'},
        ]
      }
    },
    methods: {
      update (row) {
        this.$emit('row-update', row);
      },
      remove (row) {
        this.$emit('row-remove', row);
      },
      show (item) {
        this.$emit('row-show', {id: item.id, label: item.filename, link: item.link});
      },
      generateFilename (row) {
        const suffix = row.filename.split(".").pop();
        if (!suffix) {
          return;
        }
        const scrape = (s) => (s || '').trim().replaceAll(/\W+/g, "_").toLowerCase();
        let name = '';
        function putToName(s) {
          const scraped = scrape(s);
          if (!scraped) {
            return;
          }
          if (name) {
            name += '_';
          }
          name += scraped;
        }
        putToName(row.company_name);
        putToName(row.accounting_record);
        row.filename = `${name}.${suffix}`
        this.update(row);
      },
      rowClass (item, type) {
        if (!item || type !== 'row') {
          return;
        }
        if (item._state === 'loading') {
          return 'table-secondary';
        }
        if (item._state === 'error') {
          return 'table-warning';
        }
        if (this.itemToShow && item.id === this.itemToShow.id) {
          return 'table-primary';
        }
        if (item.deleted_from_google) {
          return 'table-danger';
        }
      },
    }
  }
</script>
