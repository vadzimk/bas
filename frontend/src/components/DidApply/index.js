import Results from "../Results";
import {getDidApply, updateDidAppyRow} from "../../services/didApplyService";

export function DidApply() {
    return (
        <Results
            getData={getDidApply}
            updateRow={updateDidAppyRow}
        />
    )
}