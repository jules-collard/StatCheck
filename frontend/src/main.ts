import { bootstrapApplication } from '@angular/platform-browser';
import { App } from './app/app';
import { HttpHandlerFn, HttpRequest, provideHttpClient, withInterceptors } from '@angular/common/http';

function loggingInterceptor(request: HttpRequest<unknown>, next: HttpHandlerFn) {
  console.log('[Outgoing Request]')
  console.log(request)
  return next(request)
}

bootstrapApplication(App, {
  providers: [provideHttpClient(withInterceptors([loggingInterceptor]))]
})
  .catch((err) => console.error(err));
