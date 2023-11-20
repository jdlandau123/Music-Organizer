<script>
    import { selectedAlbum } from "../stores/collectionStore";
</script>

<div class='wrapper'>
    <!-- Update this to pull from last fm and get artwork? -->
    {#if $selectedAlbum} 
        <p>Album: {$selectedAlbum.album}</p>
        <p>Artist: {$selectedAlbum.artist}</p>
        <p>Tracklist:</p>
        {#each Object.keys($selectedAlbum.tracklist) as track}
            <p>{track}: {$selectedAlbum.tracklist[track]}</p>
        {/each}
    {:else}
        <p>Select an album from the table to view it's details</p>
    {/if}
</div>

<style>
    .wrapper {
        width: calc(40vw - 20px);
        height: calc(100vh - 255px);
        margin-top: 20px;
        overflow: scroll;
    }
</style>