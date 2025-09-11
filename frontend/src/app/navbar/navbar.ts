import { Component, inject } from '@angular/core';
import { Search } from './search/search';
import { Router, RouterLink } from '@angular/router';
import { PlayerListService } from '../search-page/player-list/player-list.service';

@Component({
  selector: 'app-navbar',
  imports: [Search, RouterLink],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css'
})
export class Navbar {
  private router = inject(Router)
  private playerListService = inject(PlayerListService)

  onSelectPlayers() {
    this.playerListService.fetch()
    this.playerListService.reset()
    this.router.navigate(['search'])
  }
}
