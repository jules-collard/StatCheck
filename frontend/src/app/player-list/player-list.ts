import { Component, computed, inject } from '@angular/core';
import { PlayerListService } from './player-list.service';
import { PlayerListItem } from './player-list-item.model';
import { PositionPipe } from "../pipes/position.pipe";
import { Router } from '@angular/router';

@Component({
  selector: 'app-player-search',
  imports: [PositionPipe],
  templateUrl: './player-list.html',
  styleUrl: './player-list.css'
})
export class PlayerList {
  private playerListService = inject(PlayerListService)
  private router = inject(Router)
  
  players = computed<PlayerListItem[]>(() => {
    return this.playerListService.filteredPlayers().slice(0,10);
  })

  isLoading = computed<boolean>(() => {return this.playerListService.isLoading()})

  onSelectListItem(id: number) {
    this.router.navigate(['players', id])    
  }
}
