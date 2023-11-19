<script>
    // @ts-nocheck
    import DataTable, { Head, Body, Row, Cell, Pagination } from '@smui/data-table';
    import Select, { Option } from '@smui/select';
    import IconButton from '@smui/icon-button';
    import { Label } from '@smui/common';
    import Checkbox from '@smui/checkbox';
    import { onMount } from 'svelte';

    const rows = ['Artist', 'Album', 'File_Format'];

    let sort = 'artist';
    let sortDirection = 'ascending';
    let sortValue = 'artist';

    let queryResults = {results: [], count: 0}
    $: collection = queryResults.results;
    $: recordsOnDevice = collection?.filter(c => c.is_on_device);

    let rowsPerPage = 25;
    let currentPage = 1;

    $: start = ((currentPage - 1) * rowsPerPage);
    $: end = Math.min(start + rowsPerPage, queryResults.count);
    $: lastPage = Math.ceil(queryResults.count / rowsPerPage);

    $: if (currentPage > lastPage) {
        currentPage = lastPage;
    }

    $: if (currentPage < 1) {
        currentPage = 1;
    }

    $: currentPage && rowsPerPage, fetchCollection();

    const fetchCollection = async () => {
        let url = `http://localhost:8000/api/albums/?page=${currentPage}&page_size=${rowsPerPage}&ordering=${sortValue}`;
        const results = await fetch(url);
        queryResults = await results.json();
    }

    onMount(() => {
		fetchCollection();
	});

    function handleSort() {
        sortValue = sortDirection === 'descending' ? `-${sort}` : sort;
        fetchCollection();
    }
</script>

<DataTable class="table" stickyHeader sortable bind:sort bind:sortDirection
            on:SMUIDataTable:sorted={handleSort}>
    <Head>
        <Row>
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
            <!-- <Cell columnId="format" sortable={false}>Format</Cell> -->
            <Cell columnId="file_format">
                <Label>Format</Label>
                <IconButton class="material-icons">arrow_upward</IconButton>
            </Cell>
        </Row>
    </Head>
    <Body>
        {#each collection as record}
            <Row>
                <Cell checkbox>
                    <Checkbox
                        bind:group={recordsOnDevice}
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
    <Pagination slot="paginate">
        <svelte:fragment slot="rowsPerPage">
          <Label>Rows Per Page</Label>
          <Select variant="outlined" bind:value={rowsPerPage} noLabel>
            <Option value={25}>25</Option>
            <Option value={50}>50</Option>
            <Option value={100}>100</Option>
          </Select>
        </svelte:fragment>
        <svelte:fragment slot="total">
          {start + 1}-{end} of {queryResults.count}
        </svelte:fragment>
     
        <IconButton
          class="material-icons"
          action="first-page"
          title="First page"
          on:click={() => (currentPage = 1)}
          disabled={currentPage === 1}>first_page</IconButton
        >
        <IconButton
          class="material-icons"
          action="prev-page"
          title="Prev page"
          on:click={() => currentPage--}
          disabled={currentPage === 1}>chevron_left</IconButton
        >
        <IconButton
          class="material-icons"
          action="next-page"
          title="Next page"
          on:click={() => currentPage++}
          disabled={currentPage === lastPage}>chevron_right</IconButton
        >
        <IconButton
          class="material-icons"
          action="last-page"
          title="Last page"
          on:click={() => (currentPage = lastPage)}
          disabled={currentPage === lastPage}>last_page</IconButton
        >
    </Pagination>
</DataTable>


<style>
    :global(.table) {
        width: 100%;
        /* max-width: 60%; */
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
</style>
