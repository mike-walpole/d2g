# Domain Configuration Guide for Dock2Gdansk

This guide explains how to configure multiple domains for your Dock2Gdansk Vercel deployment.

## 🌐 Recommended Domain Setup

### **Method 1: Vercel Dashboard (Recommended)**

1. **Deploy to Vercel first**
   ```bash
   npm run build
   vercel --prod
   ```

2. **Add domains in Vercel Dashboard:**
   - Go to your project → Settings → Domains
   - Add each domain:
     - `dock2gdansk.com` (primary)
     - `dock2gdansk.cn` (Chinese market)
     - `dock2gdansk.pl` (Polish market)
     - `www.dock2gdansk.com`
     - Any other domains you've purchased

3. **Vercel will show DNS instructions for each domain**

### **Method 2: DNS Configuration**

For each domain registrar, set up these DNS records:

#### **Root Domain (dock2gdansk.com)**
```dns
Type: A
Name: @
Value: 76.76.19.61
TTL: 300 seconds
```

#### **WWW Subdomain**
```dns
Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: 300 seconds
```

#### **Important Notes:**
- Use **A records** for root domains (`dock2gdansk.com`)
- Use **CNAME records** for subdomains (`www.dock2gdansk.com`)
- **Never use CNAME for root domains** - it breaks email and other services
- Vercel's IP addresses may change - always check the dashboard for current values

---

## 🎯 Uniform Domain Behavior

All domains now have the same behavior - they all use geolocation for language detection:

### **Domain Mapping:**
- **dock2gdansk.com** → Uses geolocation detection
- **dock2gdansk.cn** → Uses geolocation detection  
- **dock2gdansk.pl** → Uses geolocation detection
- All domains serve the same content with automatic language detection

### **Language Priority (Same for All Domains):**
1. **User manual selection** (if they clicked EN/中文)
2. **IP geolocation** (China → Chinese, others → English)
3. **English default** (fallback if geolocation fails)

---

## 🔧 DNS Provider Instructions

### **Cloudflare**
1. Add domain to Cloudflare
2. Set nameservers at registrar
3. Add DNS records:
   ```
   A @ 76.76.19.61
   CNAME www cname.vercel-dns.com
   ```
4. Set SSL/TLS to "Full"

### **Namecheap**
1. Go to Domain List → Manage
2. Advanced DNS tab
3. Add records:
   ```
   A Record: @ → 76.76.19.61
   CNAME Record: www → cname.vercel-dns.com
   ```

### **GoDaddy**
1. DNS Management
2. Add records:
   ```
   Type A: @ → 76.76.19.61
   Type CNAME: www → cname.vercel-dns.com
   ```

### **Google Domains**
1. DNS settings
2. Custom resource records:
   ```
   @ A 300 76.76.19.61
   www CNAME 300 cname.vercel-dns.com
   ```

---

## ⚡ Alternative: Redirect Method (Less Recommended)

If you prefer redirects (not recommended for SEO):

### **HTTP Redirects**
```dns
# At domain registrar
Type: URL Redirect
From: dock2gdansk.cn
To: https://dock2gdansk.com/?lang=zh
```

### **DNS-Level Redirects**
Some DNS providers offer redirect services:
- Cloudflare Page Rules
- Namecheap URL Redirect
- GoDaddy Forwarding

**Why not recommended:**
- ❌ Poor SEO (301 redirects lose link juice)
- ❌ Slower (extra HTTP round trip)
- ❌ Loses domain-specific branding
- ❌ More complex analytics tracking

---

## 🚀 Vercel Configuration

### **vercel.json (Optional)**
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        }
      ]
    }
  ]
}
```

---

## 📊 Domain Analytics

### **Google Analytics Setup**
1. Create separate properties for each domain:
   - `dock2gdansk.com` (English traffic)
   - `dock2gdansk.cn` (Chinese traffic)
   - `dock2gdansk.pl` (Polish traffic)

2. Or use one property with custom dimensions:
   ```javascript
   gtag('config', 'GA_MEASUREMENT_ID', {
     custom_map: {
       'custom_parameter_1': 'domain'
     }
   });
   ```

---

## ✅ Testing Checklist

After DNS propagation (24-48 hours):

- [ ] `dock2gdansk.com` loads correctly
- [ ] `www.dock2gdansk.com` loads correctly  
- [ ] `dock2gdansk.cn` shows Chinese by default
- [ ] `dock2gdansk.pl` shows English by default
- [ ] SSL certificates are active for all domains
- [ ] Redirects work (www → non-www or vice versa)
- [ ] Language switching works on all domains
- [ ] Analytics tracking works for all domains

---

## 🔍 Troubleshooting

### **DNS Not Propagating**
- Check propagation: https://whatsmydns.net/
- TTL too high? Lower to 300 seconds
- Clear DNS cache: `ipconfig /flushdns` (Windows) or `sudo dscacheutil -flushcache` (Mac)

### **SSL Certificate Issues**
- Wait 24-48 hours for automatic SSL
- Force SSL renewal in Vercel dashboard
- Check if DNS is pointing correctly

### **Domain Not Working**
1. Verify DNS records are correct
2. Check Vercel dashboard for domain status
3. Ensure domain is added to Vercel project
4. Check for typos in DNS records

### **Language Detection Issues**
- Clear browser localStorage
- Test with different IP addresses/VPN
- Check browser console for geolocation logs

---

## 📞 Support

If you need help:
1. Check Vercel documentation: https://vercel.com/docs/concepts/projects/domains
2. Use DNS checker tools
3. Contact your domain registrar's support
4. Check the `/debug` page on your deployment for geolocation testing