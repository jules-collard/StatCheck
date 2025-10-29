import { Component, computed, effect, inject, input as inputBinding, linkedSignal } from '@angular/core';
import { PlayerListService } from '../shared/player-list/player-list.service';
import { PlayerListItem } from './player-list-item.model';
import { PlayerFilter } from '../shared/player-list/player-filter/player-filter';
import { PositionPipe } from '../pipes/position.pipe';
import { Router } from '@angular/router';
import { TableSortService } from '../shared/table-sort.service';
import { PlayerListButton } from "../shared/player-list/player-list-button/player-list-button";


@Component({
  selector: 'app-search-page',
  imports: [PlayerFilter, PositionPipe, PlayerListButton],
  templateUrl: './search-page.html',
  styleUrl: './search-page.css',
  providers: [PlayerListService, TableSortService]
})
export class SearchPage {
  private listService = inject(PlayerListService<PlayerListItem>);
  private router = inject(Router);

  q = inputBinding.required<string | undefined>();
  searchParam = linkedSignal(() => this.q() ?? '');

  configEffect = effect(() => {
    this.listService.setConfig({
      type: 'search',
      itemsPerPage: 10
    })
  })

  playersToList = computed<PlayerListItem[]>(() => this.listService.slicedPlayers());

  onSelectListItem(id: number) {
    this.router.navigate(['players', id]);
  }
}
