<script>
  import Header from './components/Header.svelte';
  import CollectionTable from './components/CollectionTable.svelte';
  import Filters from './components/Filters.svelte';
  import AlbumDetails from './components/AlbumDetails.svelte';
</script>

<main style="display: flex; gap: 20px;">
  <div style="flex: 1">
    <Header />
    <CollectionTable />
  </div>
  <div style="width: 40%; margin-top: 65px;">
    <Filters />
    <AlbumDetails />
  </div>
</main>

<style></style>
