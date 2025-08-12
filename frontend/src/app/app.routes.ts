import { Routes } from "@angular/router";
import { PlayerPage } from "./player-page/player-page";
import { PlayerList } from "./player-list/player-list";

export const routes: Routes = [
    {
        path: 'players/:playerID',
        component: PlayerPage
    },
    {
        path: 'search',
        component: PlayerList
    }
]