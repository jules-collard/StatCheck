import { Component, computed, inject, input } from '@angular/core';
import { PlayerListItem } from './player-list-item.model';
import { PositionPipe } from "../../pipes/position.pipe";
import { Router } from '@angular/router';

@Component({
  selector: 'app-player-list',
  imports: [PositionPipe],
  templateUrl: './player-list.html',
  styleUrl: './player-list.css'
})
export class PlayerList {
  private router = inject(Router)
  
  players = input<PlayerListItem[]>([])

  onSelectListItem(id: number) {
    this.router.navigate(['players', id])    
  }
}
