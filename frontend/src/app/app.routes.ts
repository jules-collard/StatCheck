import { Routes } from "@angular/router";
import { PlayerPage } from "./player-page/player-page";
import { SearchPage } from "./search-page/search-page";
import { HomePage } from "./home-page/home-page";

export const routes: Routes = [
    {
        path: '',
        component: HomePage
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