<script>
    // @ts-nocheck
    import { queryParams, collection, selectedAlbum, recordsOnDevice } from '../stores/collectionStore';
    import DataTable, { Head, Body, Row, Cell, Pagination } from '@smui/data-table';
    import Select, { Option } from '@smui/select';
    import IconButton from '@smui/icon-button';
    import { Label } from '@smui/common';
    import Checkbox from '@smui/checkbox';
    import CircularProgress from '@smui/circular-progress';

    const rows = ['Artist', 'Album', 'File_Format'];

    let sort = 'artist';
    let sortDirection = 'ascending';
    let sortValue = 'artist';

    // $: start = (($queryParams.page - 1) * $queryParams.page_size);
    // $: end = Math.min(start + $queryParams.page_size, $collection.count);
    // $: lastPage = Math.ceil($collection.count / $queryParams.page_size);

    const handleSort = () => {
        sortValue = sortDirection === 'descending' ? `-${sort}` : sort;
        $queryParams.ordering = sortValue;
    }

    const handleCheckbox = (event) => {
        if (event.target.checked) {
            $recordsOnDevice.push(parseInt(event.target.value));
        } else {
            const index = $recordsOnDevice.indexOf(parseInt(event.target.value));
            $recordsOnDevice.splice(index, 1);
        }
        console.log($recordsOnDevice);
    }
</script>

{#if $collection && $collection.length > 0}
    <DataTable class="table" stickyHeader sortable bind:sort bind:sortDirection
                on:SMUIDataTable:sorted={handleSort}>
        <Head>
            <Row class="row">
                <Cell checkbox>
                    <Checkbox />
                </Cell>
                <Cell columnId="artist">
                    <Label>Artist</Label>
                    <IconButton class="material-icons">arrow_upward</IconButton>
                </Cell>
                <Cell columnId="album">
                    <Label>Album</Label>
                    <IconButton class="material-icons">arrow_upward</IconButton>
                </Cell>
                <Cell columnId="file_format">
                    <Label>Format</Label>
                    <IconButton class="material-icons">arrow_upward</IconButton>
                </Cell>
            </Row>
        </Head>
        <Body>
            <!-- {#each $collection.results as record} -->
            {#each $collection as record}
                <Row class="row" on:click={() => $selectedAlbum = record}>
                    <Cell checkbox>
                        <Checkbox
                            bind:checked={record.is_on_device}
                            on:change={event => handleCheckbox(event)}
                            value={record}
                            valueKey={record.id}
                        />
                    </Cell>
                    {#each rows as row}
                        <Cell class="wrap-cell">{record[row.toLowerCase()]}</Cell>
                    {/each}
                </Row>
            {/each}
        </Body>
        <!-- <Pagination slot="paginate">
            <svelte:fragment slot="rowsPerPage">
            <Label>Rows Per Page</Label>
            <Select variant="outlined" bind:value={$queryParams.page_size} noLabel>
                <Option value={25}>25</Option>
                <Option value={50}>50</Option>
                <Option value={100}>100</Option>
            </Select>
            </svelte:fragment>
            <svelte:fragment slot="total">
            {start + 1}-{end} of {$collection.count}
            </svelte:fragment>
        
            <IconButton
            class="material-icons"
            action="first-page"
            title="First page"
            on:click={() => ($queryParams.page = 1)}
            disabled={$queryParams.page === 1}>first_page</IconButton
            >
            <IconButton
            class="material-icons"
            action="prev-page"
            title="Prev page"
            on:click={() => $queryParams.page--}
            disabled={$queryParams.page === 1}>chevron_left</IconButton
            >
            <IconButton
            class="material-icons"
            action="next-page"
            title="Next page"
            on:click={() => $queryParams.page++}
            disabled={$queryParams.page === lastPage}>chevron_right</IconButton
            >
            <IconButton
            class="material-icons"
            action="last-page"
            title="Last page"
            on:click={() => ($queryParams.page = lastPage)}
            disabled={$queryParams.page === lastPage}>last_page</IconButton
            >
        </Pagination> -->
    </DataTable>
{:else}
    <div class="loading">
        <CircularProgress style="height: 45px; width: 45px;" indeterminate />
    </div>
{/if}

<style>
    :global(.table) {
        width: 100%;
        /* max-width: 60%; */
        min-height: calc(100vh - 65px);
        max-height: calc(100vh - 65px);
        overflow: scroll;
        margin-top: 65px;
        padding: 0 20px;
        text-align: left;
    }
    :global(.wrap-cell) {
        max-width: 300px;
        white-space: pre-wrap;
    }

    :global(.row):hover {
        cursor: pointer;
    }
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        min-height: calc(100vh - 65px);
        max-height: calc(100vh - 65px);
        overflow: hidden;
        margin-top: 65px;
    }

    :global(.table::-webkit-scrollbar) {
        width: 0.5rem;
    }

    :global(.table::-webkit-scrollbar-track) {
        background: #171615;
    }

    :global(.table::-webkit-scrollbar-thumb) {
        background: #b31d0c;
    }
</style>
