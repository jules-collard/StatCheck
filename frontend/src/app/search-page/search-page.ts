import { Component, computed, inject } from '@angular/core';
import { PlayerList } from './player-list/player-list';
import { PlayerListService } from './player-list/player-list.service';
import { PlayerListItem } from './player-list/player-list-item.model';

@Component({
  selector: 'app-search-page',
  imports: [PlayerList],
  templateUrl: './search-page.html',
  styleUrl: './search-page.css'
})
export class SearchPage {
  private playerListService = inject(PlayerListService)

  players = computed<PlayerListItem[]>(() => {
    return this.playerListService.filteredPlayers().slice(0,10);
  })

  isLoading = computed<boolean>(() => {return this.playerListService.isLoading()})
}
