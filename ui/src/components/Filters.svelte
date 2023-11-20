<script>
    // @ts-nocheck
    import { queryParams } from '../stores/collectionStore';
    import { onMount } from 'svelte';
    import Textfield from '@smui/textfield';
    import Select, { Option } from '@smui/select';
    import Button from '@smui/button';
    import Tooltip, { Wrapper } from '@smui/tooltip';
    import Snackbar, { Actions, Label } from '@smui/snackbar';

    let artistslist = [];
    let errorText = null;
    let snackbar;

    onMount(() => {
        fetchArtistsList();
    })

    const fetchArtistsList = async () => {
        const results = await fetch('http://localhost:8000/api/albums/get_artist_list/');
        artistslist = await results.json();
    }

    const syncWithMusicLibrary = async () => {
        const response = await fetch('http://localhost:8000/api/albums/sync_with_music_library/');
        const responseJson = await response.json();
        if (!response.ok) {
            errorText = responseJson;
            snackbar.open();
            return;
        }
    }

    const syncWithDevice = async () => {
        const response = await fetch('http://localhost:8000/api/albums/sync_with_device/');
        const responseJson = await response.json();
        if (!response.ok) {
            errorText = responseJson;
            snackbar.open();
            return;
        }
    }
</script>

<Textfield bind:value={$queryParams.search} label="Search" style="width: calc(40vw - 20px)"></Textfield>

<Select bind:value={$queryParams.artist} label="Filter By Artist" style="width: calc(40vw - 20px)">
    <Option value={null}></Option>
    {#each artistslist as artist}
      <Option value={artist}>{artist}</Option>
    {/each}
</Select>

<div style="display: flex; justify-content: space-around; margin-top: 20px;">
    <Wrapper>
        <Button variant={'raised'} on:click={syncWithMusicLibrary}>
            Sync With Music Library
        </Button>
        <Tooltip xPos={'center'}>Sync the app's database with your music library</Tooltip>
    </Wrapper>
    <Wrapper>
        <Button variant={'raised'} on:click={syncWithDevice}>
            Sync With Device
        </Button>
        <Tooltip xPos={'center'}>Sync the device with the selected albums</Tooltip>
    </Wrapper>
</div>

<Snackbar bind:this={snackbar}>
    <Label>{errorText}</Label>
</Snackbar>
