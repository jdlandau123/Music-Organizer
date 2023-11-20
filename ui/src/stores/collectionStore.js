import { writable } from "svelte/store";

const collection = writable({results: [], count: 0});

const selectedAlbum = writable(null);

const queryParams = writable({
    page: 1,
    page_size: 25,
    ordering: 'artist',
    artist: null,
    search: null
});

const fetchCollection = async (params) => {
    let url = `http://localhost:8000/api/albums/?`;
    Object.keys(params).forEach((p, index) => {
        if (params[p]) {
            url += index > 0 ? `&${p}=${params[p]}` : `${p}=${params[p]}`;
        }
    })
    const results = await fetch(url);
    collection.set(await results.json());
}

queryParams.subscribe(params => fetchCollection(params));

export { queryParams, collection, selectedAlbum };
