<script>
    // @ts-nocheck
    import { queryParams, recordsOnDevice } from '../stores/collectionStore';
    import { onMount } from 'svelte';
    import Textfield from '@smui/textfield';
    import Select, { Option } from '@smui/select';
    import Button from '@smui/button';
    import Tooltip, { Wrapper } from '@smui/tooltip';
    import Snackbar, { Label } from '@smui/snackbar';
    import LinearProgress from '@smui/linear-progress';
    import Dialog, { Title, Content } from '@smui/dialog';

    let artistslist = [];
    let errorText = null;
    let snackbar;

    let totalProgressCount = 0;
    let progress = 0;
    let dialogOpen = false;
    let dialogTitle = '';
    let pollingInterval = null;

    let searchText = '';

    $: progressDecimal = progress / totalProgressCount;
    
    $: if (progressDecimal === 1) {
        clearInterval(pollingInterval);
        setTimeout(() => dialogOpen = false, 3000);
    }

    onMount(() => {
        fetchArtistsList();
    })

    const search = () => {
        setTimeout(() => $queryParams.search = searchText, 500);
    }

    const fetchArtistsList = async () => {
        const results = await fetch('http://localhost:8000/api/albums/get_artist_list/');
        artistslist = await results.json();
    }

    const syncWithMusicLibrary = async () => {
        dialogTitle = 'Syncing With Music Library';
        const response = await fetch('http://localhost:8000/api/albums/sync_with_music_library/');
        const responseJson = await response.json();
        if (!response.ok) {
            errorText = responseJson;
            snackbar.open();
            return;
        }
        dialogOpen = true;
        pollingInterval = setInterval(() => pollProgress(responseJson), 500);
    }

    const syncDevice = async () => {
        dialogTitle = 'Syncing To Device';
        const response = await fetch('http://localhost:8000/api/albums/sync_with_device/', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ids: $recordsOnDevice})
        });
        const responseJson = await response.json();
        if (!response.ok) {
            errorText = responseJson;
            snackbar.open();
            return;
        }
        dialogOpen = true;
        pollingInterval = setInterval(() => pollProgress(responseJson), 500);
    }

    const pollProgress = async (jobId) => {
        const response = await fetch('http://localhost:8000/api/albums/get_sync_progress/', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({key: jobId})
        });
        if (!response.ok) {
            dialogOpen = false;
            progress = 0;
            errorText = 'Could not fetch progress';
        }
        const progressResponse = await response.json();
        if (totalProgressCount === 0) {
            totalProgressCount = progressResponse.total;
        }
        progress = progressResponse.completed;
    }
</script>

<Textfield bind:value={searchText} on:input={search} label="Search" style="width: calc(40vw - 20px)"></Textfield>

<Select bind:value={$queryParams.artist} label="Filter By Artist" style="width: calc(40vw - 20px)">
    <Option value={null}></Option>
    {#each artistslist as artist}
        <Option value={artist}>{artist}</Option>
    {/each}
</Select>

<!-- TODO: figure out why adding another dropdown breaks the UI ??  -->
<!-- <div style="display: flex; justify-content: space-between; width: calc(40vw - 20px); gap: 20px;">
    <Select bind:value={$queryParams.artist} label="Filter By Artist" style="width: 50%">
        <Option value={null}></Option>
        {#each artistslist as artist}
            <Option value={artist}>{artist}</Option>
        {/each}
    </Select>
    <Select bind:value={$queryParams.file_format} label="Filter By File Type" style="width: 50%">
        <Option value={null}></Option>
        <Option value={'MP3'}>MP3</Option>
        <Option value={'FLAC'}>FLAC</Option>
        <Option value={'WAV'}>WAV</Option>
    </Select>
</div> -->

<div style="display: flex; justify-content: space-around; margin-top: 20px;">
    <Wrapper>
        <Button variant={'raised'} on:click={syncWithMusicLibrary}>
            Sync With Music Library
        </Button>
        <Tooltip xPos={'center'}>Sync the app's database with your music library</Tooltip>
    </Wrapper>
    <Wrapper>
        <Button variant={'raised'} on:click={syncDevice}>
            Sync Device
        </Button>
        <Tooltip xPos={'center'}>Sync the device with the selected albums</Tooltip>
    </Wrapper>
</div>

<Snackbar bind:this={snackbar}>
    <Label>{errorText}</Label>
</Snackbar>

<Dialog bind:open={dialogOpen} surface$style="width: 1000px;">
  <Title>{dialogTitle}</Title>
  <Content>
    <LinearProgress progress={progressDecimal} style="width: 75%%;" />
    <p>{progress} of {totalProgressCount} albums completed</p>
  </Content>
</Dialog>
