const initialState = {};
export default function imgDetail(preState = initialState, action) {
    const { type, data } = action;

    switch (type) {
        case 'imgDetail':
            return data;
        default:
            return preState;
    }
}