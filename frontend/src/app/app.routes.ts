import { Routes } from "@angular/router";
import { PlayerPage } from "./player-page/player-page";
import { SearchPage } from "./search-page/search-page";

export const routes: Routes = [
    {
        path: '',
        component: SearchPage
    },
    {
        path: 'players/:playerID',
        component: PlayerPage
    },
    {
        path: 'search',
        component: SearchPage
    }
]