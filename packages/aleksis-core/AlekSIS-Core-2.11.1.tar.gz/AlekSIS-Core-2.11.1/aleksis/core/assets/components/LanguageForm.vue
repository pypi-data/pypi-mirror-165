<template>
  <form method="post" ref="form" :action="action" id="language-form">
    <v-text-field
      v-show="false"
      name="csrfmiddlewaretoken"
      :value="csrf_value"
      type="hidden"
    ></v-text-field>
    <v-text-field
      v-show="false"
      name="next"
      :value="next_url"
      type="hidden"
    ></v-text-field>
    <v-text-field
      v-show="false"
      v-model="language"
      name="language"
      type="hidden"
    ></v-text-field>
    <v-menu offset-y>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          depressed
          v-bind="attrs"
          v-on="on"
          color="primary"
        >
          <v-icon icon color="white">mdi-translate</v-icon>
          {{ language }}
        </v-btn>
      </template>
      <v-list id="language-dropdown" class="dropdown-content">
        <v-list-item-group
          v-model="language"
          color="primary"
        >
          <v-list-item v-for="language_option in items" :key="language_option[0]" :value="language_option[0]" @click="submit(language_option[0])">
            <v-list-item-title>{{ language_option[1] }}</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-menu>
  </form>
</template>

<script>
  export default {
    data: () => ({
        items: JSON.parse(document.getElementById("language-info-list").textContent),
        language: JSON.parse(document.getElementById("current-language").textContent),
    }),
    methods: {
        submit: function (new_language) {
            this.language = new_language;
            this.$nextTick(() => {
                this.$refs.form.submit();
            });
        },
    },
    props: ["action", "csrf_value", "next_url"],
    name: "language-form",
  }
</script>
