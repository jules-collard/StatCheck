import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { PlayerList } from './player-list/player-list';
import { PlayerListService } from './player-list/player-list.service';
import { PlayerListItem } from './player-list/player-list-item.model';
import { SearchService } from './search.service';
import { PlayerFilter } from './player-filter/player-filter';

@Component({
  selector: 'app-search-page',
  imports: [PlayerList, PlayerFilter],
  templateUrl: './search-page.html',
  styleUrl: './search-page.css'
})
export class SearchPage implements OnInit {
  private playerListService = inject(PlayerListService)
  private searchService = inject(SearchService)
  playersPerPage = 10;

  currPage = computed<number>(() => {
    return this.searchService.currPage()
  })

  filteredPlayers = computed<PlayerListItem[]>(() => {
    return this.playerListService.filteredPlayers()
  })

  playersToList = computed<PlayerListItem[]>(() => {
    return this.playerListService.filteredPlayers().slice(this.searchService.currPage() * this.playersPerPage, (this.searchService.currPage() + 1) * this.playersPerPage)
  })

  maxPages = computed<number>(() => {
    return Math.ceil(this.filteredPlayers().length / this.playersPerPage)
  })

  firstPage() { this.searchService.firstPage() }
  nextPage() { this.searchService.nextPage() }
  prevPage() { this.searchService.prevPage() }
  lastPage() {this.searchService.goToPage(this.maxPages() - 1)}

  ngOnInit(): void {
    this.playerListService.fetch()
  }
}
