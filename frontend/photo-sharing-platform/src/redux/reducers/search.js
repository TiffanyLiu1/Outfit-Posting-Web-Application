const initialState = [];
export default function mainSearch(preState = initialState, action) {
    const { type, data } = action;

    switch (type) {
        case 'searchResult':
            return data;
        default:
            return preState;
    }
}