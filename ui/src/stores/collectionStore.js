// @ts-nocheck
import { writable } from "svelte/store";

const collection = writable([]);

const selectedAlbum = writable(null);

const recordsOnDevice = writable([]);

const queryParams = writable({
    // page: 1,
    // page_size: 25,
    ordering: 'artist',
    artist: null,
    search: null,
    file_format: null
});

const fetchCollection = async (params) => {
    let url = `http://localhost:8000/api/albums/?`;
    Object.keys(params).forEach((p, index) => {
        if (params[p]) {
            url += index > 0 ? `&${p}=${params[p]}` : `${p}=${params[p]}`;
        }
    })
    const results = await fetch(url);
    const collectionJson = await results.json();
    collection.set(collectionJson);
    // recordsOnDevice.set(collectionJson.results.filter(c => c.is_on_device).map(a => a.id));
    recordsOnDevice.set(collectionJson.filter(c => c.is_on_device).map(a => a.id));
}

queryParams.subscribe(params => fetchCollection(params));

export { queryParams, collection, selectedAlbum, recordsOnDevice };
