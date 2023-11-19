<script>
  import Header from './components/Header.svelte';
  import CollectionTable from './components/CollectionTable.svelte';
  import Filters from './components/Filters.svelte';
</script>

<main style="display: flex; gap: 20px;">
  <div style="flex: 1">
    <Header />
    <CollectionTable />
  </div>
  <div style="width: 40%; margin-top: 65px;">
    <Filters />
  </div>
</main>

<style></style>
