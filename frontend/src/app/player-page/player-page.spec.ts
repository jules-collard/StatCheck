import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayerPage } from './player-page';

describe('PlayerPage', () => {
  let component: PlayerPage;
  let fixture: ComponentFixture<PlayerPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlayerPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PlayerPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
