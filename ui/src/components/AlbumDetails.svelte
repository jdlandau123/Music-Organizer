<script>
    import { selectedAlbum } from "../stores/collectionStore";

    let artworkUrl = null;

    const queryLastFm = async () => {
        const response = await fetch(
            `https://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=${import.meta.env.VITE_LASTFM_API_KEY}&artist=${$selectedAlbum.artist}&album=${$selectedAlbum.album}&format=json`
        );
        if (!response.ok) {
            console.error('Error fetching artowork');
            artworkUrl = null;
            return;
        }
        const albumInfo = await response.json();
        artworkUrl = albumInfo.album.image.find(i => i.size === 'extralarge')['#text'];
    }

    selectedAlbum.subscribe(() => {
        if ($selectedAlbum) {
            queryLastFm()
        }
    })
</script>

<div class='wrapper'>
    <!-- Update this to pull from last fm and get artwork -->
    {#if $selectedAlbum} 
        {#if artworkUrl}
        <div style="display: flex; justify-content: center;">
            <img src={artworkUrl} alt={$selectedAlbum.album + ' artwork'} style="margin: auto" />
        </div>
        {/if}
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
        --webkit-scrollbar: #080808;
    }

    :global(.wrapper::-webkit-scrollbar) {
        width: 0.5rem;
    }

    :global(.wrapper::-webkit-scrollbar-track) {
        background: #171615;
    }

    :global(.wrapper::-webkit-scrollbar-thumb) {
        background: #b31d0c;
    }
</style>